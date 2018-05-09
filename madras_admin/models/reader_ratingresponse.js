'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('reader_ratingresponse', {
    'data': {
      type: DataTypes.STRING,
    },
    'applicant_id': {
      type: DataTypes.INTEGER,
    },
    'reader_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'reader_ratingresponse',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

