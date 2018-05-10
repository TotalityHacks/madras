'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('checkin_checkingroup', {
    'checked_in': {
      type: DataTypes.BOOLEAN,
    },
    'uuid': {
      type: DataTypes.UUID,
      primaryKey: true 
    },
  }, {
    tableName: 'checkin_checkingroup',
    underscored: true,
    timestamps: false,
    schema: process.env.DATABASE_SCHEMA,
  });

  Model.associate = (models) => {
    Model.belongsTo(models.registration_applicant, {
      foreignKey: 'applicant_id',
      
      as: '_applicant_id',
    });
    
  };

  return Model;
};

