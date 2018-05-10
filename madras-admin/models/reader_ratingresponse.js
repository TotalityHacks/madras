'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_ratingresponse', {
    'data': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'reader_ratingresponse',
    
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.registration_applicant, {
      foreignKey: 'applicant_id',
      
      as: '_applicant_id',
    });
    
    Model.belongsTo(models.reader_reader, {
      foreignKey: 'reader_id',
      
      as: '_reader_id',
    });
    
  };

  return Model;
};

